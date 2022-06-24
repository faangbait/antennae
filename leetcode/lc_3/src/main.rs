use std::collections::HashMap;

pub struct Solution {}

impl Solution {
    /// Given a string s, find the length of the longest substring without repeating characters.
    pub fn length_of_longest_substring(s: String) -> i32 {
        let mut max_len = 0;
        let mut start = 0;
        let mut map = HashMap::new();
        for (i, c) in s.chars().enumerate() {
            if map.contains_key(&c) {
                start = std::cmp::max(start, map[&c] + 1);
            }
            map.insert(c, i);
            max_len = std::cmp::max(max_len, i - start + 1);
        }
        max_len as i32
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn simple() {
        assert_eq!(Solution::length_of_longest_substring("abcd".to_string()), 4);
        assert_eq!(Solution::length_of_longest_substring("abcabcbb".to_string()), 3);
        assert_eq!(Solution::length_of_longest_substring("bbbbb".to_string()), 1);
        assert_eq!(Solution::length_of_longest_substring("pwwkew".to_string()), 3);
        assert_eq!(Solution::length_of_longest_substring("abba".to_string()), 2);
    }
}

fn main() {}
