locals {
  name_prefix = "${var.project_name}-${terraform.workspace}"

  frontend_container_name = "frontend"
  backend_container_name  = "backend"

  frontend_container_port = 3000
  backend_container_port  = 9000

  frontend_ecr_repo_name = "${var.project_name}-frontend"
  backend_ecr_repo_name  = "${var.project_name}-backend"

  domain_name   = "srikanthreddy.fun"
  app_subdomain = "ai"
  app_fqdn      = "${local.app_subdomain}.${local.domain_name}"
}
