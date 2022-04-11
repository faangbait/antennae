pub struct Solution {}

fn main() {
    Solution::fizz_buzz(60);
}

use std::thread;
impl Solution {
    pub fn fizz_buzz(n: i32) -> Vec<String> {
        let mut handles = vec![];
            (1..n+1).for_each(|i| {
                let handle = thread::spawn(move|| {
                    match i % 15 {
                        0 => "FizzBuzz".to_string(),
                        3 => "Fizz".to_string(),
                        5 => "Buzz".to_string(),
                        6 => "Fizz".to_string(),
                        9 => "Fizz".to_string(),
                        10=> "Buzz".to_string(),
                        12=> "Fizz".to_string(),
                        _ => i.to_string(),
                    }
                });
                handles.push(handle);
            });

        handles.into_iter().map(|f| f.join().unwrap()).collect()
    }
}
