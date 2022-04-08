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

fn main() {
    let sol = Solution::roman_to_int;
    print!("III: {} [want: 3]\n", sol("III".to_string()));
    print!("LVIII: {} [want: 58]\n", sol("LVIII".to_string()));
    print!("MCMXCIV: {} [want: 1994]\n", sol("MCMXCIV".to_string()));
    print!(
        "MMCMXCVIII: {} [want: 2998]\n",
        sol("MMCMXCVIII".to_string())
    );
}
