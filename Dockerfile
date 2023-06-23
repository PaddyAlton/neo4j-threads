FROM python:3.10-slim

# create a non-root user/usergroup
RUN addgroup --gid 10001 --system nonroot \
 && adduser  --uid 10000 --system --ingroup nonroot --home /threads threads-admin

# switch working directory to non-root user's home
WORKDIR /threads

# install our dependencies
RUN python3 -m pip install -U pip && pip install pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN pipenv install --system

# add the working directory to the PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/threads"

# shouldn't run the application as root
USER threads-admin

# bring in the source code
COPY src src

# run the application
ENTRYPOINT ["uvicorn", "src:app"]
CMD ["--host", "0.0.0.0", "--port", "8765"]
