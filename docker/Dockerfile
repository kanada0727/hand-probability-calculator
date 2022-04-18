#---#
FROM python:3.9-slim-buster as base

###-----------------------------------------------
### pdm builder
###-----------------------------------------------
FROM base as pdm-builder
RUN apt update && apt install -y curl
RUN curl -sSL https://raw.githubusercontent.com/pdm-project/pdm/main/install-pdm.py | python3 -


###-----------------------------------------------
### project base
###-----------------------------------------------
FROM base as project-base
###### --- install pdm ---
COPY --from=pdm-builder /root/.local /root/.local
COPY --from=pdm-builder /root/.bashrc /root/.bashrc
ENV PATH $PATH:/root/.local/bin
ENV PYTHONPATH /root/.local/share/pdm/venv/lib/python3.9/site-packages/pdm/pep582
###-----------------------------------------------
### development
###-----------------------------------------------
FROM project-base as development

###### --- install nodejs for jupyter ---
COPY --from=node:15.6-buster-slim /usr/local/bin/node /usr/local/bin/node
COPY --from=node:15.6-buster-slim /usr/local/bin/nodejs /usr/local/bin/nodejs
COPY --from=node:15.6-buster-slim /usr/local/lib/node_modules/ /usr/local/lib/node_modules/
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm

###### --- install basic commands ---
RUN apt update && apt install -y procps git vim curl tig

###### --- edit bash prompt message to specify location (inside container) cf: https://qiita.com/hmmrjn/items/60d2a64c9e5bf7c0fe60
RUN echo "PS1='\[\e[1;35m\](INSIDE_CONTAINER)\[\e[0m\] \u:\w \$ '" >> ~/.bashrc

###### --- setting project path ---
###### NOTE: put this code in the end to share cache with other projects
ENV PROJECT_PATH /root/hand-probability-calculator

##### environment variables for jupyterlab
ENV JUPYTERLAB_DIR ${PROJECT_PATH}/__pypackages__/3.9/share/jupyter/lab
ENV JUPYTERLAB_WORKSPACES_DIR ${PROJECT_PATH}/__pypackages__/3.9/share/jupyter/lab
ENV JUPYTERLAB_SETTINGS_DIR ${PROJECT_PATH}/__pypackages__/3.9/share/jupyter/lab

WORKDIR $PROJECT_PATH
ENV WORKDIR $PROJECT_PATH
CMD ["/bin/bash"]

###-----------------------------------------------
### production builder
###-----------------------------------------------
FROM project-base as production-builder

###### --- setting project path ---
ENV PROJECT_PATH /root/hand-probability-calculator
WORKDIR $PROJECT_PATH

###### --- install python packages ---
COPY ./pdm.lock ./pdm.lock
COPY ./pyproject.toml ./pyproject.toml
RUN pdm install --prod

###-----------------------------------------------
### production
###-----------------------------------------------
FROM base as production

###### --- setting project path ---
ENV PROJECT_PATH /root/hand-probability-calculator
WORKDIR $PROJECT_PATH

COPY ./ ./

###### --- copy python runtime ---
COPY --from=production-builder $PROJECT_PATH/.venv/ ./.venv
ENV PATH $PATH:$PROJECT_PATH/.venv/bin/python3

CMD ["/bin/bash"]
