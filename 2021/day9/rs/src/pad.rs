use ndarray::{Array, ArrayBase, Axis, Data, Dimension, Slice};

/// Pad the edges of an array with zeros.
///
/// `pad_width` specifies the length of the padding at the beginning
/// and end of each axis.
///
/// **Panics** if `arr.ndim() != pad_width.len()`.
pub fn pad<A, S, D>(
    arr: &ArrayBase<S, D>,
    pad_width: Vec<[usize; 2]>,
    const_value: A,
) -> Array<A, D>
where
    A: Clone,
    S: Data<Elem = A>,
    D: Dimension,
{
    assert_eq!(
        arr.ndim(),
        pad_width.len(),
        "Array ndim must match length of `pad_width`."
    );

    // Compute shape of final padded array.
    let mut padded_shape = arr.raw_dim();
    for (ax, (&ax_len, &[pad_lo, pad_hi])) in arr.shape().iter().zip(&pad_width).enumerate() {
        padded_shape[ax] = ax_len + pad_lo + pad_hi;
    }

    let mut padded = Array::from_elem(padded_shape, const_value);
    let padded_dim = padded.raw_dim();
    {
        // Select portion of padded array that needs to be copied from the
        // original array.
        let mut orig_portion = padded.view_mut();
        for (ax, &[pad_lo, pad_hi]) in pad_width.iter().enumerate() {
            orig_portion.slice_axis_inplace(
                Axis(ax),
                Slice::from(pad_lo as isize..padded_dim[ax] as isize - (pad_hi as isize)),
            );
        }
        // Copy the data from the original array.
        orig_portion.assign(arr);
    }
    padded
}

pub fn pad_2d<A, S, D>(
    arr: &ArrayBase<S, D>,
    pad_width: usize,
    const_value: A,
) -> Array<A, D>
where
    A: Clone,
    S: Data<Elem = A>,
    D: Dimension,
{
    pad(arr, vec![[pad_width; 2], [pad_width; 2]], const_value)
}