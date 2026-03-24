variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
  description = "Public subnet 1 CIDR"
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_subnet_cidr_2" {
  description = "Public subnet 2 CIDR"
  type        = string
  default     = "10.0.2.0/24"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "ai-chatbot"
}

variable "openai_api_key" {
  description = "OpenAI API key stored in SSM Parameter Store"
  type        = string
  sensitive   = true
  default     = "OPENAI_API_KEY"
}
# ⚠️ DO NOT hardcode secrets here
# variable "openai_api_key" {
#   sensitive = true
# }

########################################################

# ✅ HARD CODED ECR IMAGES (what you wanted)
variable "frontend_image" {
  default = "511552693812.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-frontend:latest"
}

variable "backend_image" {
  default = "511552693812.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-backend:latest"
}
