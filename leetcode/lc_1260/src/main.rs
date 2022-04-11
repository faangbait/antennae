pub struct Solution {}

fn main(){
    let sol = Solution::shift_grid;
    assert_eq!(sol(vec![vec![1,2,3],vec![4,5,6],vec![7,8,9]],1),vec![vec![9,1,2],vec![3,4,5],vec![6,7,8]]);
    assert_eq!(sol(vec![vec![3,8,1,9],vec![19,7,2,5],vec![4,6,11,10],vec![12,0,21,13]],4),vec![vec![12,0,21,13],vec![3,8,1,9],vec![19,7,2,5],vec![4,6,11,10]]);
}

// Given a 2D grid of size m x n and an integer k. You need to shift the grid k times.

// In one shift operation:

// Element at grid[i][j] moves to grid[i][j + 1].
// Element at grid[i][n - 1] moves to grid[i + 1][0].
// Element at grid[m - 1][n - 1] moves to grid[0][0].
// Return the 2D grid after applying shift operation k times.
impl Solution {
    pub fn shift_grid(grid: Vec<Vec<i32>>, k: i32) -> Vec<Vec<i32>> {
        // let mut decomposed = vec![];
        // let row_len = grid[0].len();
        // let height = grid.len();

        // for i in grid {
        //     for j in i {
        //         decomposed.push(j);
        //     }
        // };

        // (0..k).for_each(|_i| {let val = decomposed.pop().unwrap(); decomposed.insert(0,val);} );

        // let mut recomposed = vec![];
        // (0..height).for_each(|_i| recomposed.push(vec![]));
        // for (idx, val) in decomposed.iter_mut().enumerate() {
        //     println!("{}, {}", idx, val);
        //     recomposed[idx / row_len].push(*val);
        // }

        // recomposed

        let mut decomposed = grid.concat();
        let len = decomposed.len();
        decomposed.rotate_right(k as usize % len);
        decomposed.chunks(grid[0].len())
            .map(|s| s.to_vec())
            .collect()
    }
}
