# This is the default target, which will be built when 
# you invoke make
current_dir = $(shell pwd)
container_name = decky-stream-waker-backend
.PHONY: all
all:
	docker build -t $(container_name) .
	docker run --rm -i -v $(current_dir):/backend -v $(current_dir)/out:/backend/out $(container_name)
rebuild:
	docker rmi $(container_name)
	docker build -t $(container_name) .