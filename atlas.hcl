variable "token" {
    type    = string
    default = getenv("DB_TOKEN")
}

variable "subdomain" {
    type = string
    default = getenv("DB_SUBDOMAIN")
}

env "turso" {
  url     = "libsql+wss://${var.subdomain}.turso.io?authToken=${var.token}"
  exclude = ["_litestream*"]
}

