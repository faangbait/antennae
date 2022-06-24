pub struct Solution {}

impl Solution {

    /// A happy number is a number defined by the following process: 
    /// Starting with any positive integer, replace the number by the sum of the squares of its digits,
    /// and repeat the process until the number equals 1 (where it will stay), or it loops endlessly
    /// in a cycle which does not include 1. Those numbers for which this process ends in 1 are happy numbers.
    pub fn is_happy(n: i32) -> bool {
        let mut n = n;
        let mut sum = 0;
        while n > 0 {
            sum += (n % 10).pow(2);
            n /= 10;
        }
        if sum == 1 {
            return true;
        }
        if sum == 4 {
            return false;
        }
        Solution::is_happy(sum)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn simple() {
        assert_eq!(true, Solution::is_happy(1));
        assert_eq!(false, Solution::is_happy(2));
        assert_eq!(true, Solution::is_happy(7));
        assert_eq!(false, Solution::is_happy(8));
        assert_eq!(true, Solution::is_happy(13));
        assert_eq!(false, Solution::is_happy(14));
        assert_eq!(true, Solution::is_happy(19));
        assert_eq!(false, Solution::is_happy(2));
    }
}

fn main() {}
