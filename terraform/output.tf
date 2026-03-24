output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = aws_lb.main.dns_name
}

output "app_url" {
  description = "URL for the chatbot application"
  value       = "https://${local.app_fqdn}"
}

output "acm_certificate_arn" {
  description = "ACM certificate ARN for the app hostname"
  value       = aws_acm_certificate.app.arn
}
