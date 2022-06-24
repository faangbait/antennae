pub struct Solution {}

/// Leetcode Problem #09 - Palindrome Number
/// Given an integer x, return true if x is palindrome integer.
/// An integer is a palindrome when it reads the same backward as forward.
impl Solution {
    pub fn is_palindrome(x: i32) -> bool {
        let sx = x.to_string();
        
        for (i, c) in sx.chars().enumerate() {
            if c != sx.chars().nth(sx.len() - i - 1).unwrap() {
                return false;
            }
            if i > sx.len() / 2 {
                return true;
            }
        }
        return true;
    }
}

fn main() {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn simple() {
        assert_eq!(Solution::is_palindrome(123), false);
        assert_eq!(Solution::is_palindrome(121), true);
        assert_eq!(Solution::is_palindrome(123456789), false);
        assert_eq!(Solution::is_palindrome(123454321), true);
    }
    #[test]
    pub fn even() {
        assert_eq!(Solution::is_palindrome(1221), true);
        assert_eq!(Solution::is_palindrome(1222), false);
    }
}
