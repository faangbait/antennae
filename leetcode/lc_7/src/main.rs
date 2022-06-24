pub struct Solution {}

impl Solution {
    /// Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-2^31, 2^31 - 1], then return 0.
    pub fn reverse(x: i32) -> i32 {

        let mut num = x.checked_abs().unwrap_or(0);
        if num == 0 { return 0 };
        
        let mut result:i32 = 0;
        while num > 0 {
            let digit = num % 10;
            num /= 10;
            result = result.checked_mul(10)
                .and_then(|r| r.checked_add(digit))
                .unwrap_or(0);
        };


        if x.is_negative() {
            result.checked_neg().unwrap_or(0)
        } else {
            result
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn simple() {
        assert_eq!(Solution::reverse(123), 321);
    }

    #[test]
    pub fn neg() {
        assert_eq!(Solution::reverse(-123), -321);
    }
    #[test]
    pub fn overflow() {
        assert_eq!(Solution::reverse(2147483647), 0);
    }
    #[test]
    pub fn overflow2() {
        assert_eq!(Solution::reverse(-2147483648), 0);
    }
    #[test]
    pub fn overflow3() {
        assert_eq!(Solution::reverse(-2147483642), 0);
    }
    
    #[test]
    pub fn zero() {
        assert_eq!(Solution::reverse(0), 0);
    }
    #[test]
    pub fn leading_zero() {
        assert_eq!(Solution::reverse(120), 21);
    }
    #[test]
    pub fn leading_zero2() {
        assert_eq!(Solution::reverse(1203000), 3021);
    }
    #[test]
    pub fn non_leading_zero() {
        assert_eq!(Solution::reverse(1203), 3021);
    }

}

fn main() {}
