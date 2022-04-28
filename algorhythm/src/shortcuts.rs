use actix_web::{HttpResponse, error};
use actix_web::http::{ header,StatusCode };
use tera::Tera;
/// Renders a response to an incoming HTTP Request
pub fn render(
    // request: HttpRequest,
    template_name: &str,
    context: &tera::Context,
    content_type: header::ContentType
) -> Result<HttpResponse, actix_web::Error> {
    
    let mut tera = match Tera::new("templates/**/*") {
        Ok(t) => t,
        Err(e) => {
            println!("Parsing error(s): {}", e);
            ::std::process::exit(1);
        }
    };

    tera.autoescape_on(vec![".raw"]);
    
    let rendered = tera.render(template_name, context);
    let status = StatusCode::OK;
    match rendered {
        Ok(body) => {
            let mut resp = HttpResponse::Ok();
            resp.status(status);
            resp.insert_header(content_type);
            Ok(resp.body(body))
        }
        Err(err) => Err(error::ErrorNotImplemented(err))
    }
}
