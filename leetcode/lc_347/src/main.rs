
pub struct Solution {}

fn main() {
    let sol = Solution::top_k_frequent;
    assert_eq!(sol(vec![1,1,1,2,2,3], 2),vec![1,2]);
    assert_eq!(sol(vec![1], 1),vec![1]);
    assert_eq!(sol(vec![0,2,3,3,4,5,6,6,6,6], 2),vec![6,3]);
    assert_eq!(sol(vec![-1,-1], 1),vec![-1]);
    assert_eq!(sol(vec![1,2],2),vec![1,2]);
    assert_eq!(sol(vec![1,1,1,2,2,2,3,3,3],3), vec![1,2,3]);
    
}

// Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.
impl Solution {
    pub fn top_k_frequent(nums: Vec<i32>, k: i32) -> Vec<i32> {
        println!("-----{}-----", k);
        if k as usize == nums.len() { return nums; }
        let vals = nums.clone();
        
        let mut hashmap = std::collections::HashMap::<i32,i32>::new();
        
        for v in vals {
            let count = hashmap.entry(v).or_insert(0);
            *count += 1;
            println!("k: {}, v: {}", v, count);
        }

        let mut biggest: Vec<(i32,i32)> = vec![];
        for (k,v) in hashmap {
            biggest.push((k,v));
        }
        
        biggest.sort_unstable_by_key(|(_,v)| -1 * v);
        biggest.truncate(k as usize);
        let mut res = vec![];
        for (k,_) in biggest { res.push(k);}
        res
    }
}
