pub struct Solution {}

fn main() {
    let sol = Solution::number_of_steps;
    assert_eq!(sol(14),6);
    assert_eq!(sol(8),4);
    assert_eq!(sol(123),12);
    assert_eq!(sol(0),0);
}

///Given an integer num, return the number of steps to reduce it to zero.
/// In one step, if the current number is even, you have to divide it by 2, otherwise, you have to subtract 1 from it.
impl Solution {
    /// this is an O(1) binary solution
    /// 14 = 1110 -> /= 2
    /// 7 = 111 -> -= 1
    /// 6 = 110 > /= 2
    /// 3 = 11...
    /// 123 = 1111011 -> count of "1s" = 6; count of "bits" = 7; ans = 7+6-1
    pub fn number_of_steps(num: i32) -> i32 {
        ((
            num.count_ones() * 2 +
            (num.count_zeros() - num.leading_zeros())
        ).max(1) - 1) as i32
    }
}
