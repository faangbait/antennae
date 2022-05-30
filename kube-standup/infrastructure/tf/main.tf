terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  shared_credentials_file = "~/.aws/credentials"
}

variable "routes" {
    type = object({
        glass = list(string)
        prod = list(string)
    })

    default = {
        glass = [
            "fetch.news",
            "search.news"
        ]
        prod = []
    }
}


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

variable "dynamic_dns" {
    type = list(string)
    default = ["ipv4-is-about-to-be.strangled.net"]
}


resource "aws_route53_record" "glass" {
    zone_id     = var.zones.glass
    name        = each.key
    type        = "CNAME"
    ttl         = 5
    records     = var.dynamic_dns
    for_each    = toset(var.routes.glass)
}

resource "aws_route53_record" "prod" {
    zone_id     = var.zones.prod
    name        = each.key
    type        = "CNAME"
    ttl         = 5
    records     = var.dynamic_dns
    for_each    = toset(var.routes.prod)
}

resource "aws_route53_record" "glass_txt" {
    zone_id     = var.zones.glass
    name        = ""
    type        = "TXT"
    ttl         = 300
    records     = var.txt_records.glass
}

resource "aws_route53_record" "glass_mx" {
    zone_id     = var.zones.glass
    name        = ""
    type        = "MX"
    ttl         = 3600
    records     = ["10 mail.tutanota.de"]
}

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

