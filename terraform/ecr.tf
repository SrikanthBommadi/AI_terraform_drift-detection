# resource "aws_ecr_repository" "frontend" {
#   name                 = local.frontend_ecr_repo_name
#   image_tag_mutability = "MUTABLE"

#   image_scanning_configuration {
#     scan_on_push = false
#   }

#   lifecycle {
#     # Keep Docker images safe if you destroy/recreate the rest of the stack.
#     prevent_destroy = true
#   }

#   tags = {
#     Name    = "${local.name_prefix}-frontend-ecr"
#     Project = var.project_name
#   }
# }

# resource "aws_ecr_repository" "backend" {
#   name                 = local.backend_ecr_repo_name
#   image_tag_mutability = "MUTABLE"

#   image_scanning_configuration {
#     scan_on_push = false
#   }

#   lifecycle {
#     # Keep Docker images safe if you destroy/recreate the rest of the stack.
#     prevent_destroy = true
#   }

#   tags = {
#     Name    = "${local.name_prefix}-backend-ecr"
#     Project = var.project_name
#   }
# }