package main

import (
	"bytes"
	"errors"
	"github.com/libp2p/go-buffer-pool"
	"github.com/quic-go/quic-go/http3"
	"io"
	"log"
	"net/http"
	"os"
)

var p pool.BufferPool
var ErrWAF = errors.New("WAF")

func main() {
	go func() {
		err := http.ListenAndServeTLS(":8080", "./server.crt", "./server.key", &mux{})
		log.Fatalln(err)
	}()
	go func() {
		err := http3.ListenAndServeQUIC(":8080", "./server.crt", "./server.key", &mux{})
		log.Fatalln(err)
	}()
	select {}
}

type mux struct {
}

func (*mux) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		_, _ = w.Write([]byte("Hello D^3CTF 2025,I'm tidy quic in web."))
		return
	}
	if r.Method != http.MethodPost {
		w.WriteHeader(400)
		return
	}

	var buf []byte
	length := int(r.ContentLength)
	if length == -1 {
		var err error
		buf, err = io.ReadAll(textInterrupterWrap(r.Body))
		if err != nil {
			if errors.Is(err, ErrWAF) {
				w.WriteHeader(400)
				_, _ = w.Write([]byte("WAF"))
			} else {
				w.WriteHeader(500)
				_, _ = w.Write([]byte("error"))
			}
			return
		}
	} else {
		buf = p.Get(length)
		defer p.Put(buf)
		rd := textInterrupterWrap(r.Body)
		i := 0
		for {
			n, err := rd.Read(buf[i:])
			if err != nil {
				if errors.Is(err, io.EOF) {
					break
				} else if errors.Is(err, ErrWAF) {
					w.WriteHeader(400)
					_, _ = w.Write([]byte("WAF"))
					return
				} else {
					w.WriteHeader(500)
					_, _ = w.Write([]byte("error"))
					return
				}
			}
			i += n
		}
	}
	if !bytes.HasPrefix(buf, []byte("I want")) {
		_, _ = w.Write([]byte("Sorry I'm not clear what you want."))
		return
	}
	item := bytes.TrimSpace(bytes.TrimPrefix(buf, []byte("I want")))
	if bytes.Equal(item, []byte("flag")) {
		_, _ = w.Write([]byte(os.Getenv("FLAG")))
	} else {
		_, _ = w.Write(item)
	}
}

type wrap struct {
	io.ReadCloser
	ban []byte
	idx int
}

func (w *wrap) Read(p []byte) (int, error) {
	n, err := w.ReadCloser.Read(p)
	if err != nil && !errors.Is(err, io.EOF) {
		return n, err
	}
	for i := 0; i < n; i++ {
		if p[i] == w.ban[w.idx] {
			w.idx++
			if w.idx == len(w.ban) {
				return n, ErrWAF
			}
		} else {
			w.idx = 0
		}
	}
	return n, err
}

func textInterrupterWrap(rc io.ReadCloser) io.ReadCloser {
	return &wrap{
		rc, []byte("flag"), 0,
	}
}
