FROM public.ecr.aws/lambda/python:3.11.2023.11.13.10

WORKDIR /.

COPY requirements.txt .

RUN pip3 install -r requirements.txt

# Copy function code
COPY discordnote.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "discordnote.lambda_handler" ]