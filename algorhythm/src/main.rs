use actix_web::{middleware, web, App, HttpServer};
use tera::Tera;
use tokio;

mod shortcuts;
mod responses;
mod views;

use responses::ErrorResponse;

#[tokio::main]
async fn main() -> std::io::Result<()> {
    std::env::set_var("RUST_LOG", "actix_web=info");
    env_logger::init();
    println!("Listening on: 127.0.0.1:3000, open browser and visit have a try!");

    HttpServer::new(|| {
        let tera = Tera::new(concat!(env!("CARGO_MANIFEST_DIR"), "/templates/**/*")).unwrap();

        App::new()
        .app_data(web::Data::new(tera))
        .wrap(middleware::Logger::default()) // enable logger
        .service(web::resource("/").route(web::get().to(views::index)))
        .service(web::scope("").wrap(responses::error_handlers(ErrorResponse::NotFound)))
    })
    .bind(("127.0.0.1", 3000))?
    .run()
    .await
}
