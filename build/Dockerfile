FROM python:3.10-alpine as base_image

##################################

FROM base_image as builder_image
RUN apk add --no-cache build-base
RUN apk add --no-cache linux-headers
RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH
COPY ./gree/requirements.txt /requirements.txt
RUN source /venv/bin/activate && \
	python -m pip install -r /requirements.txt

##################################

FROM base_image as final_image

# SETUP USER
ARG USER_NAME=appuser
ARG USER_ID=9001
RUN adduser -u ${USER_ID} -S ${USER_NAME}

# SETUP PYTHON MODULES
COPY --from=builder_image /venv /venv
ENV PATH=/venv/bin:$PATH

# SETUP APP
COPY --chmod=755 ./gree /gree
WORKDIR /gree

USER ${USER_ID}:${USER_ID}

# SETUP ENTRYPOINT
COPY --chmod=755 ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "run" ]
