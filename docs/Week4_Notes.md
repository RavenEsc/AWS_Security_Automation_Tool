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

Update: I have discovered how to solve the RunTime error. I simply have to remove TFC's enviornment from the equation by running it locally. It functioned properly after I made a shorcut to the current python RunTime and ran the 'terraform plan' on my Windows Machine. And it WORKS! Currently, I am unsure if it will run the same if I run it off of GitHub's enviornment, I plan to put it to the test soon!

Update: Welp, I just tested it and now I don't know if I can keep up this "trying to stick to my TFC VCS configuration" charade. It is entirely an enviornment issue and it doesn't look like it will be fixed (I just sent an email to a Hashicorp contact). I might have to deal with API tokens and go for an API-Driven GitHub Workflow. That way, I guess I have even more control over issues that come my way with GitHub actions at my fingertips. I still am unsure why building a module was the answer as it requires a .zip file to be made and placed in the GitHub Repository. So unless I can some how only make a temporary dependencies.zip file and run it purely off of terraform (which is still sketchy because I am not in charge of the environment) it looks like I will have to switch to the GitHub API Workflow. (I could go without terraform cloud at this point, but why change it if it will do the same thing, but with extra steps....??!!)
New theory: Run only off of GitHub with Actions, make a workflow file like before, but link it to OIDC for GitHub in AWS to provide a more flexible link between the two! It is worth a shot, as I have forgotten what the main issue is between GitHub and AWS or if I had one at all. 

Update: For now I thin it would be best to re-attempt the API-Driven workflow. I plan on testing it first thing tomorrow morning.