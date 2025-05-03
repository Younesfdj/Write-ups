def reverse_pairwise_swap(data: bytes) -> bytes:
    arr = bytearray(data)
    for i in range(0, len(arr) - 1, 2):
        arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return bytes(arr)


if __name__ == "__main__":
    original = b"enux{s_C4bek_d1whts_m0_esa_mnot_3hs_d1}e" # Read from memory
    swapped = reverse_pairwise_swap(original)

    print("flag:", swapped.decode())   
