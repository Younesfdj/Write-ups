import os
import shutil
import subprocess
import tempfile

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# uv run uvicorn main:app --reload

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def serve_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit")
async def handle_upload(request: Request, file: UploadFile = File(...)):
    if not file.filename.endswith('.bundle'):
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "success": False,
                "error_title": "Invalid File Type",
                "output": "Please upload a valid Git bundle file (.bundle extension)"
            },
            status_code=400
        )

    # Use a NamedTemporaryDirectory instead of manual directory creation
    with tempfile.TemporaryDirectory(prefix="git_verification_") as temp_dir:
        try:
            # Save the uploaded bundle file
            bundle_path = os.path.join(temp_dir, file.filename)
            with open(bundle_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Create a directory for the verification process
            local_dir = os.path.join(temp_dir, "local")
            git_dir = os.path.join(local_dir, ".git")

            # Execute the verification steps
            # Step 1: mkdir local
            os.makedirs(local_dir, exist_ok=True)

            # Step 2: git clone --mirror your-bundle.bundle local/.git
            clone_result = subprocess.run(
                ["git", "clone", "--mirror", bundle_path, git_dir],
                capture_output=True,
                text=True,
                check=False
            )

            if clone_result.returncode != 0:
                return templates.TemplateResponse(
                    "result.html",
                    {
                        "request": request,
                        "success": False,
                        "error_title": "Failed to clone the bundle",
                        "output": clone_result.stderr
                    },
                    status_code=400
                )

            # Step 3: cd local & git config --bool core.bare false
            config_result = subprocess.run(
                ["git", "config", "--bool", "core.bare", "false"],
                cwd=local_dir,
                capture_output=True,
                text=True,
                check=False
            )

            if config_result.returncode != 0:
                return templates.TemplateResponse(
                    "result.html",
                    {
                        "request": request,
                        "success": False,
                        "error_title": "Failed to set git config",
                        "output": config_result.stderr
                    },
                    status_code=400
                )

            # Step 4: git rev-list 36a168b7942eedf14b33912db25357cb254457e9
            rev_list_result = subprocess.run(
                ["git", "rev-list", "36a168b7942eedf14b33912db25357cb254457e9"],
                cwd=local_dir,
                capture_output=True,
                text=True,
                check=False
            )

            if rev_list_result.returncode != 0:
                return templates.TemplateResponse(
                    "result.html",
                    {
                        "request": request,
                        "success": False,
                        "error_title": "Failed to find the required commit",
                        "output": rev_list_result.stderr
                    },
                    status_code=400
                )

            # Step 5: git checkout 36b1a27 && ./run.sh
            checkout_result = subprocess.run(
                ["git", "checkout", "36a168b7942eedf14b33912db25357cb254457e9"],
                cwd=local_dir,
                capture_output=True,
                text=True,
                check=False
            )

            if checkout_result.returncode != 0:
                return templates.TemplateResponse(
                    "result.html",
                    {
                        "request": request,
                        "success": False,
                        "error_title": "Failed to checkout the commit",
                        "output": checkout_result.stderr
                    },
                    status_code=400
                )

            # Execute run.sh
            run_script_path = os.path.join(local_dir, "run.sh")

            run_result = subprocess.run(
                ["./run.sh"],
                cwd=local_dir,
                capture_output=True,
                text=True,
                check=False
            )

            # Return the result of the verification
            if run_result.returncode == 0:
                output = run_result.stdout.strip() or "Verification completed successfully!"
                return templates.TemplateResponse(
                    "result.html",
                    {
                        "request": request,
                        "success": True,
                        "output": output
                    }
                )
            else:
                return templates.TemplateResponse(
                    "result.html",
                    {
                        "request": request,
                        "success": False,
                        "error_title": "Script execution failed",
                        "output": run_result.stderr
                    },
                    status_code=400
                )

        except Exception as e:
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "success": False,
                    "error_title": "An unexpected error occurred",
                    "output": str(e)
                },
                status_code=500
            )