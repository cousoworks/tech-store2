import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useCart } from '../contexts/CartContext';
import api from '../services/api';
import { FaShoppingCart, FaStar } from 'react-icons/fa';

const ProductDetailPage = () => {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reviewText, setReviewText] = useState('');
  const [rating, setRating] = useState(5);
  const { id } = useParams();
  const { addToCart } = useCart();

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/products/${id}`);
        // Adaptar la estructura de datos para que funcione con la interfaz
        const adaptedProduct = {
          id: response.data.id,
          name: response.data.nombre,
          description: response.data.descripcion || '',
          price: response.data.precio,
          stock: response.data.cantidad,
          image_url: response.data.image_url,
          created_at: response.data.fecha_creacion,
          avg_rating: 5, // Valor por defecto ya que no tenemos reseñas en la DB actual
          review_count: 0, // Valor por defecto ya que no tenemos reseñas en la DB actual
          reviews: [] // Valor por defecto ya que no tenemos reseñas en la DB actual
        };
        setProduct(adaptedProduct);
        setError(null);
      } catch (err) {
        setError('Failed to load product details.');
        console.error('Error fetching product:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleAddToCart = () => {
    if (product) {
      addToCart({ ...product, quantity: 1 });
    }
  };

  const handleReviewSubmit = async (e) => {
    e.preventDefault();
    
    // Como no tenemos API de reseñas con la DB actual, solo mostraremos un mensaje
    alert('La funcionalidad de reseñas no está disponible en esta versión.');
    setReviewText('');
    setRating(5);
  };

  if (loading) return <div className="flex justify-center items-center min-h-screen"><div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div></div>;
  
  if (error) return <div className="container mx-auto px-4 py-8 text-center text-red-500">{error}</div>;
  
  if (!product) return <div className="container mx-auto px-4 py-8 text-center">Product not found</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col md:flex-row gap-8">
        {/* Product Image */}
        <div className="md:w-1/2">
          <img 
            src={product.image_url || 'https://via.placeholder.com/500x500?text=No+Image'} 
            alt={product.name}
            className="w-full h-auto object-cover rounded-lg shadow-md"
          />
        </div>
        
        {/* Product Details */}
        <div className="md:w-1/2">
          <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
          
          <div className="flex items-center mb-4">
            <div className="flex text-yellow-400">
              {Array.from({ length: 5 }).map((_, i) => (
                <FaStar 
                  key={i} 
                  className={i < Math.round(product.avg_rating || 0) ? 'text-yellow-400' : 'text-gray-300'} 
                />
              ))}
            </div>
            <span className="ml-2 text-gray-600">
              ({product.review_count || 0} reviews)
            </span>
          </div>
          
          <p className="text-2xl font-semibold text-blue-600 mb-4">${product.price.toFixed(2)}</p>
          
          <p className="text-gray-700 mb-6">{product.description}</p>
          
          {product.stock > 0 ? (
            <>
              <p className="text-green-600 mb-4">In Stock ({product.stock} available)</p>
              <button
                onClick={handleAddToCart}
                className="flex items-center justify-center bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors w-full md:w-auto"
              >
                <FaShoppingCart className="mr-2" />
                Add to Cart
              </button>
            </>
          ) : (
            <p className="text-red-600 mb-4">Out of Stock</p>
          )}
        </div>
      </div>
      
      {/* Reviews Section */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold mb-6">Customer Reviews</h2>
        
        {/* Add Review Form */}
        <div className="bg-gray-50 p-6 rounded-lg shadow mb-8">
          <h3 className="text-lg font-semibold mb-4">Leave a Review</h3>
          <form onSubmit={handleReviewSubmit}>
            <div className="mb-4">
              <label className="block mb-2 text-gray-700">Rating</label>
              <div className="flex items-center">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    className={`text-2xl mr-1 ${
                      star <= rating ? 'text-yellow-400' : 'text-gray-300'
                    }`}
                  >
                    <FaStar />
                  </button>
                ))}
              </div>
            </div>
            <div className="mb-4">
              <label className="block mb-2 text-gray-700">Your Review</label>
              <textarea
                value={reviewText}
                onChange={(e) => setReviewText(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg"
                rows="4"
                required
              ></textarea>
            </div>
            <button
              type="submit"
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Submit Review
            </button>
          </form>
        </div>
        
        {/* Review List */}
        {product.reviews && product.reviews.length > 0 ? (
          <div className="space-y-6">
            {product.reviews.map((review) => (
              <div key={review.id} className="border-b pb-4">
                <div className="flex items-center mb-2">
                  <div className="flex text-yellow-400">
                    {Array.from({ length: 5 }).map((_, i) => (
                      <FaStar 
                        key={i} 
                        className={i < review.rating ? 'text-yellow-400' : 'text-gray-300'} 
                      />
                    ))}
                  </div>
                  <span className="ml-4 font-medium">{review.user_name}</span>
                  <span className="ml-4 text-gray-500 text-sm">
                    {new Date(review.created_at).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-gray-700">{review.text}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No reviews yet. Be the first to leave a review!</p>
        )}
      </div>
    </div>
  );
};

export default ProductDetailPage;
