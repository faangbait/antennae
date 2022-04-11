pub struct Solution {}

fn main() {
}

impl Solution {
    pub fn fizz_buzz(n: i32) -> Vec<String> {
        (1..n+1).map(|x| { match x % 15 {
            0 => "FizzBuzz".to_string(),
            3 => "Fizz".to_string(),
            5 => "Buzz".to_string(),
            6 => "Fizz".to_string(),
            9 => "Fizz".to_string(),
            10=> "Buzz".to_string(),
            12=> "Fizz".to_string(),
            _ => x.to_string(),
        }}).collect()
    }
}
