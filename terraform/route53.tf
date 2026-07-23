resource "aws_route53_zone" "main" {
  count = var.enable_dns ? 1 : 0
  name  = var.domain_name

  tags = {
    Project = var.project_name
  }
}

resource "aws_acm_certificate" "site" {
  count             = var.enable_dns ? 1 : 0
  provider          = aws.us_east_1
  domain_name       = var.domain_name
  validation_method = "DNS"

  tags = {
    Project = var.project_name
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  count   = var.enable_dns ? 1 : 0
  zone_id = aws_route53_zone.main[0].zone_id
  name    = tolist(aws_acm_certificate.site[0].domain_validation_options)[0].resource_record_name
  type    = tolist(aws_acm_certificate.site[0].domain_validation_options)[0].resource_record_type
  records = [tolist(aws_acm_certificate.site[0].domain_validation_options)[0].resource_record_value]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "site" {
  count                   = var.enable_dns ? 1 : 0
  provider                = aws.us_east_1
  certificate_arn         = aws_acm_certificate.site[0].arn
  validation_record_fqdns = [aws_route53_record.cert_validation[0].fqdn]
}

resource "aws_route53_record" "site" {
  count   = var.enable_dns ? 1 : 0
  zone_id = aws_route53_zone.main[0].zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.site.domain_name
    zone_id                = aws_cloudfront_distribution.site.hosted_zone_id
    evaluate_target_health = false
  }
}
