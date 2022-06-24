
pub struct Solution {}

fn main() {}

impl Solution {
    pub fn find_median_sorted_arrays(nums1: Vec<i32>, nums2: Vec<i32>) -> f64 {
        let sum_length= nums1.len() + nums2.len();
        let mut slice = [nums1, nums2].concat();

        let nth = slice.select_nth_unstable(sum_length / 2);
        let median = nth.1.clone() as f64;

        if sum_length % 2 == 0 {
            (nth.0.select_nth_unstable(nth.0.len()-1).1.clone() as f64 + median) / 2.0
        } else {
            median
        }
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    pub fn find_median_sorted_arrays() {
        let sol = Solution::find_median_sorted_arrays;

        assert_eq!(sol(vec![1,3], vec![2]), 2 as f64);
        assert_eq!(sol(vec![1,2], vec![3,4]), 2.5 as f64);
    }
}
