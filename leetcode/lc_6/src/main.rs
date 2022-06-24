pub struct Solution {}

impl Solution {
    /// The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)
    /// P   A   H   N
    /// A P L S I I G
    /// Y   I   R
    /// Write the code that will take a string and make this conversion given a number of rows:
    pub fn convert(s: String, num_rows: i32) -> String {
        if num_rows == 1 { return s; }
        let mut res = vec![String::new(); num_rows as usize];

        let mut row: i32 = 0;
        let mut down = false;

        for ch in s.chars() {
            res[row as usize].push(ch);
            if row == 0 || row == num_rows - 1 {
                down = !down;
            }
            row += if down { 1 } else { -1 };
        };
        res.concat()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn one_per() {
        assert_eq!(Solution::convert("ABCDEFG".to_string(),7), "ABCDEFG".to_string());
    }

    #[test]
    pub fn one_row() {
        assert_eq!(Solution::convert("AB".to_string(),1), "AB".to_string());
    }

    #[test]
    pub fn three() {
        assert_eq!(Solution::convert("PAYPALISHIRING".to_string(), 3), "PAHNAPLSIIGYIR".to_string());
    }

    #[test]
    pub fn four() {
        assert_eq!(Solution::convert("PAYPALISHIRING".to_string(), 4), "PINALSIGYAHRPI".to_string());

    }
    
    #[test]
    pub fn single() {
        assert_eq!(Solution::convert("A".to_string(), 1), "A".to_string());
    }

}

fn main() {}
