terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

#
# ~/.aws/credentials
# [kubernetes]
# aws_access_key_id=
# aws_secret_access_key=
#
provider "aws" {
  profile = "kubernetes"
  region = "us-east-1"
  shared_credentials_file = "~/.aws/credentials"
}

#
# This should be the only block that needs changing regularly...
#
variable "routes" {
    type = object({
        glass = list(string)
        prod = list(string)
    })

    default = {
        glass = [
            "auth",
            "fetch.news",
            "search.news",
            "shorts.news",
            "videos.news",
            "docs.news",
            "zines.news",
            "audio.news",
            "library.news",
            "conf.news",
            "etl.news",
            "xmit.news",
            "i18n.news",
            "mon.home",
            "request.home",
            "ui.home",
            "dashboard.public",
        ]
        prod = []
    }
}

#
# Route53 Dev/Prod Environment Setup
#
# glass: dev env hosted zone id
# prod: prod env hosted zone id
#
variable "zones" {
    type = object({
        glass   = string
        prod    = string
    })

    default = {
        glass = "Z010939671A5NCHBBBCH"
        prod = "Z05575802ULDZNGHPUH6L"
    }
}

# Add custom TXT records to your domains
variable "txt_records" {
    type = object({
        glass   = list(string)
        prod    = list(string)
    })

    default = {
        glass = [
            "v=spf1 include:spf.tutanota.de -all",
            "t-verify=11acbe5e629f8a8d102afdde3fc41e96",
            "google-site-verification=sUe3qihNuz7ICXGgqHrmsJcfZr1Zm2hzyvgLtvuRaDE"
            ]
        prod = [
            "v=spf1 include:amazonses.com ~all",
            ]
    }
}

#
# This should be a DNS record that points to your server.
# e.g. afraid.org or another dynamic DNS provider
#
variable "dynamic_dns" {
    type = list(string)
    default = ["ipv4-is-about-to-be.strangled.net"]
}

# Don't change
resource "aws_route53_record" "glass" {
    zone_id     = var.zones.glass
    name        = each.key
    type        = "CNAME"
    ttl         = 5
    records     = var.dynamic_dns
    for_each    = toset(var.routes.glass)
}

# Don't change
resource "aws_route53_record" "prod" {
    zone_id     = var.zones.prod
    name        = each.key
    type        = "CNAME"
    ttl         = 5
    records     = var.dynamic_dns
    for_each    = toset(var.routes.prod)
}

# Don't change
resource "aws_route53_record" "glass_txt" {
    zone_id     = var.zones.glass
    name        = ""
    type        = "TXT"
    ttl         = 300
    records     = var.txt_records.glass
}

# Change for custom MX records on dev
resource "aws_route53_record" "glass_mx" {
    zone_id     = var.zones.glass
    name        = ""
    type        = "MX"
    ttl         = 3600
    records     = ["10 mail.tutanota.de"]
}

# Change for custom DMARC records on dev
resource "aws_route53_record" "glass_email" {
    zone_id     = var.zones.glass
    name        = each.key
    type        = "CNAME"
    ttl         = 3600
    records     = each.value
    for_each    = {
        _dmarc = ["v=DMARC1;p=quarantine;adkim=s"]
        _mta-sts = ["mta-sts.tutanota.de."]
    }
}

# Change for custom DKIM records on dev
resource "aws_route53_record" "glass_dkim" {
    zone_id     = var.zones.glass
    name        = "${each.key}._domainkey"
    type        = "CNAME"
    ttl         = 3600
    records     = each.value
    for_each    = {
        s1 = ["s1.domainkey.tutanota.de."]
        s2 = ["s2.domainkey.tutanota.de."]
    }
}


