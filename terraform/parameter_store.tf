resource "aws_ssm_parameter" "chatbot_openai_api_key" {
  name        = "/${local.name_prefix}/OPENAI_API_KEY"
  description = "OpenAI API key for chatbot backend"
  type        = "String"
  value       = var.openai_api_key

  tags = {
    Project = var.project_name
  }
}
