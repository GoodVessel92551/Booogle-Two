if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('./sw.js').then(function(reg) {
      console.log('Successfully registered service worker', reg);
      this.addEventListener('fetch', function (event) {
      });
  }).catch(function(err) {
      console.warn('Error whilst registering service worker', err);
  });
}
this.addEventListener('fetch', function (event) {
});


