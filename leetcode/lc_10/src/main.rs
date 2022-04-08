pub struct Solution {}

/// Leetcode Problem #10 - Palindrome Number
/// Given an integer x, return true if x is palindrome integer.
/// An integer is a palindrome when it reads the same backward as forward.
impl Solution {
    pub fn is_palindrome(x: i32) -> bool {
        let stringvec = x.to_string();
        let chars = stringvec.chars();
        let reverse = chars.rev();

        if stringvec.chars().eq(reverse) {
            return true;
        }
        return false;
    }
}

fn main() {
    let sol = Solution::is_palindrome;
    print!("123: {} [want: false]\n", sol(123));
    print!("121: {} [want: true]\n", sol(121));
    print!("1234567890: {} [want: false]\n", sol(1234567890));
    print!("123454321: {} [want: true]\n", sol(123454321));
}
