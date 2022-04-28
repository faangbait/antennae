use actix_web::{HttpResponse, web, Result};
use actix_web::body::BoxBody;
use actix_web::dev::ServiceResponse;
use actix_web::http::StatusCode;
use actix_web::http::header::ContentType;
use actix_web::middleware::{ErrorHandlers, ErrorHandlerResponse};
use tera::Tera;

pub enum ErrorResponse {
    NotFound,
}
// Custom error handlers, to return HTML responses when an error occurs.
pub fn error_handlers(err: ErrorResponse) -> ErrorHandlers<BoxBody> {
    
    let err_type = match err {
        ErrorResponse::NotFound => (StatusCode::NOT_FOUND, not_found)
    };

    ErrorHandlers::new().handler(err_type.0, err_type.1)
}

// Error handler for a 404 Page not found error.
fn not_found<B>(res: ServiceResponse<B>) -> Result<ErrorHandlerResponse<BoxBody>> {
    let response = get_error_response(&res, "Page not found");
    Ok(ErrorHandlerResponse::Response(ServiceResponse::new(
        res.into_parts().0,
        response.map_into_left_body(),
    )))
}

// Generic error handler.
fn get_error_response<B>(res: &ServiceResponse<B>, error: &str) -> HttpResponse {
    let request = res.request();

    let fallback = |e: &str| {
        HttpResponse::build(res.status())
            .content_type(ContentType::plaintext())
            .body(e.to_string())
    };

    let tera = request.app_data::<web::Data<Tera>>().map(|t| t.get_ref());
    match tera {
        Some(tera) => {
            let mut context = tera::Context::new();
            context.insert("error", error);
            context.insert("status_code", res.status().as_str());
            let body = tera.render("error.html", &context);

            match body {
                Ok(body) => HttpResponse::build(res.status())
                    .content_type(ContentType::html())
                    .body(body),
                Err(_) => fallback(error),
            }
        }
        None => fallback(error),
    }
}
