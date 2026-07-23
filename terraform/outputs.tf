output "s3_bucket_name" {
  value = aws_s3_bucket.site.id
}

output "cloudfront_distribution_id" {
  value = aws_cloudfront_distribution.site.id
}

output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.site.domain_name
}

output "website_url" {
  value = var.enable_dns ? "https://${var.domain_name}" : "https://${aws_cloudfront_distribution.site.domain_name}"
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.visitor_counter.api_endpoint
}
