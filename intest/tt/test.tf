module "s3_bucket" {
  source = "../modules/terraform-aws-s3-bucket"

  bucket = "jjhbucket-test"
  acl    = "private"
  region = "ap-northeast-2"
  tags = {
    System = "jjhtest"
  }
}

#module "cdn" {
#  source             = "git::https://github.com/cloudposse/terraform-aws-cloudfront-cdn.git?ref=master"
#  namespace          = "cp"
#  stage              = "prod"
#  name               = "app"
#  origin_domain_name = module.s3_bucket.this_s3_bucket_bucket_domain_name 
#}