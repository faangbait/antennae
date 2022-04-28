use actix_web::http::header::ContentType;
use actix_web::{HttpResponse, Error};

use crate::shortcuts;

pub async fn index() -> Result<HttpResponse, Error> {
    shortcuts::render("root.html", &tera::Context::new(), ContentType::html())
}
