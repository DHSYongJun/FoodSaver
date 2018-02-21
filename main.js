
new Vue({
  el: '#app',
  data () {
    return {
      items: [
        {
        title: 'Biscuits',
        items: [
          { title: 'Date of Expiry:', date: '25/1/18'},
          { title: 'Date of Purchase:', date: '25/1/18'}
        ]
        },
        {
          title: 'Apples',
          items: [
            { title: 'Date of Expiry:', date: '30/1/18'},
            { title: 'Date of Purchase:', date: '25/1/18'}
          ]
        },
        {
          title: 'Mushrooms',
          items: [
            { title: 'Date of Expiry:', date: '25/1/18'},
            { title: 'Date of Purchase:', date: '20/1/18'}
          ]
        },
      ]
    }
  }
})
