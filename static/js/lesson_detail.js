$(document).ready(function () {
      const stars = document.querySelectorAll('.star');
      let rating = 0;
  
      stars.forEach((star) => {
          star.addEventListener('click', () => {
              rating = parseInt(star.getAttribute('data-rating'));
              setRating();
              console.log('Star clicked')
          });
  
          star.addEventListener('mouseenter', () => {
              const hoverRating = parseInt(star.getAttribute('data-rating'));
              highlightStars(hoverRating);
          });
  
          star.addEventListener('mouseleave', () => {
              highlightStars(rating);
          });
      });
  
      function highlightStars(num) {
          stars.forEach((star, index) => {
              if (index < num) {
                  star.classList.add('clicked');
              } else {
                  star.classList.remove('clicked');
              }
          });
      }
  
      function setRating() {
          // You can send the 'rating' variable to your server using AJAX
          // For example, using jQuery AJAX
          $.ajax({
              type: 'POST',
              url: '/curriculum/rate-lecture/', // URL to handle the rating on the server
              data: {
                  csrfmiddlewaretoken: '{{ csrf_token }}',
                  rating: rating,
                  lesson_id: '{{ lessons.lesson_id }}' // Pass the lesson ID or relevant identifier
              },
              success: function (response) {
                  // Handle the server response here, if needed
              },
              error: function () {
                  // Handle errors, if any
              }
          });
        }
});    