
pub struct Solution {}

impl Solution {
    /// Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer (similar to C/C++'s atoi function).
    /// The algorithm for myAtoi(string s) is as follows:
    /// Read in and ignore any leading whitespace.
    /// Check if the next character (if not already at the end of the string) is '-' or '+'. Read this character in if it is either. This determines if the final result is negative or positive respectively. Assume the result is positive if neither is present.
    /// Read in next the characters until the next non-digit character or the end of the input is reached. The rest of the string is ignored.
    /// Convert these digits into an integer (i.e. "123" -> 123, "0032" -> 32). If no digits were read, then the integer is 0. Change the sign as necessary (from step 2).
    /// If the integer is out of the 32-bit signed integer range [-2^31, 2^31 - 1], then clamp the integer so that it remains in the range. Specifically, integers less than -2^31 should be clamped to -2^31, and integers greater than 2^31 - 1 should be clamped to 2^31 - 1.
    /// Return the integer as the final result.
    pub fn my_atoi(s: String) -> i32 {
        let s = s.trim();

        match s.parse() {
            Ok(i) => i,
            Err(e) => match e.kind() {
                std::num::IntErrorKind::Empty => 0,
                std::num::IntErrorKind::InvalidDigit => {
                    if s.starts_with("-") {
                        if let Some(t) = s.chars().skip(1).next() {
                            if t.is_digit(10) {
                                return Self::my_atoi(s.chars().skip(1).collect::<String>()).checked_neg().unwrap_or(i32::MIN);
                            } else { return 0; }
                        } else { return 0;}
                    }

                    if s.starts_with("+") {
                        if let Some(t) = s.chars().skip(1).next() {
                            if t.is_digit(10) {
                                return Self::my_atoi(s.chars().skip(1).collect::<String>());
                            } else { return 0; }
                        } else { return 0;}
                    }
                    
                    return Self::my_atoi(s.chars().fuse()
                        .take_while(|&c| c.is_digit(10))
                        .collect::<String>());
                },
                std::num::IntErrorKind::PosOverflow => return i32::MAX,
                std::num::IntErrorKind::NegOverflow => return i32::MIN,
                std::num::IntErrorKind::Zero => return 0,
                _ => panic!("Unhandled error"),
            },
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    pub fn leading_whitespace() {
        assert_eq!(Solution::my_atoi(String::from("   42")), 42);
    }

    #[test]
    pub fn leading_sign() {
        assert_eq!(Solution::my_atoi(String::from("   -42")), -42);
    }

    #[test]
    pub fn leading_sign_and_whitespace() {
        assert_eq!(Solution::my_atoi(String::from("   +42")), 42);
    }

    #[test]
    pub fn clamp() {
        assert_eq!(Solution::my_atoi(String::from("   -2147483648")), -2147483648);
    }

    #[test]
    pub fn clamp2() {
        assert_eq!(Solution::my_atoi(String::from("2147483648")), 2147483647);
    }

    #[test]
    pub fn words() {
        assert_eq!(Solution::my_atoi(String::from("4193 with words 30")), 4193);
    }
    
    #[test]
    pub fn simple_parse() {
        assert_eq!(Solution::my_atoi(String::from("0042")), 42);
    }

    #[test]
    pub fn leading_words() {
        assert_eq!(Solution::my_atoi(String::from("words and 987")), 0);
    }

    #[test]
    pub fn two_signs() {
        assert_eq!(Solution::my_atoi(String::from("+-332")), 0);
    }

    #[test]
    pub fn negative_words() {
        assert_eq!(Solution::my_atoi(String::from("-faangbait01")), 0);
    }

    #[test]
    pub fn just_sign() {
        assert_eq!(Solution::my_atoi(String::from("+")), 0);
    }
}

fn main() {}
