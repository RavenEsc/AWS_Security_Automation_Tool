# Project SAT

Update: Finished up the six Goals set in week 3

Applied to the Associate HanaByte Program.

Find a fix in GitHub Actions to change the lambda python RunTime after the terraform is completed running

- Find out how to run a command after a terraform workflow with VCS connection is completed

Otherwise, Work on running a check on all RESOURCE policies for the wildcard(*) character/ overly permissive policy permission

## Meeting

- Make an AWS Org from Terraform
- Landing Zone: AWS Accounts auto, predeployed, monitoring

- Creating a new AWS account

- Kuberenetes, A Whole New World, & Amazon EKS
- A container orchestration conductor

____________________

Update: I can not use GitHub Actions with Terraform VCS, and the current lambda module is not compatible with the Version Control TFC. So the only current option is to create a local module. Time to learn how to make a module!

Update: Looks like making a module would not fix the issue of avoiding .zip files like the lambda layer as it was originally intended. I will have took look into other ways of installing the dependencies. For now, I am running tests on the original issue from the lambda module. Hopefully I discover the issue. But I am now dealing with credential inaccess again?! Lots of prayer is going into this!