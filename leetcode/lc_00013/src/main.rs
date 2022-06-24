pub struct Solution {}

/// Leetcode Problem #13 - Roman to Integer
/// Given a roman numeral, convert it to an integer
/// Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.
impl Solution {
    pub fn roman_to_int(s: String) -> i32 {
        let s_iter = s.chars();
        let mut last_elem = '_';
        let mut sum = 0;
        for elem in s_iter {
            sum += match elem {
                'I' => 1,
                'V' => match last_elem {
                    'I' => 3,
                    _ => 5,
                },
                'X' => match last_elem {
                    'I' => 8,
                    _ => 10,
                },
                'L' => match last_elem {
                    'X' => 30,
                    _ => 50,
                },
                'C' => match last_elem {
                    'X' => 80,
                    _ => 100,
                },
                'D' => match last_elem {
                    'C' => 300,
                    _ => 500,
                },
                'M' => match last_elem {
                    'C' => 800,
                    _ => 1000,
                },
                _ => 0,
            };
            last_elem = elem;
        }
        return sum;
    }
}

fn main() {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn simple() {
        assert_eq!(Solution::roman_to_int("III".to_string()), 3);
        assert_eq!(Solution::roman_to_int("LVIII".to_string()), 58);
    }

    #[test]
    pub fn complex() {
        assert_eq!(Solution::roman_to_int("MCMXCIV".to_string()), 1994);
        assert_eq!(Solution::roman_to_int("MMCMXCVIII".to_string()), 2998);
    }
}
