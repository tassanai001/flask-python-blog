<template>
  <div>
    <div class="home--create--btn">
      <b-button type="is-info" @click="onCreate">
        <font-awesome-icon icon="plus" />
      </b-button>
    </div>
    <div
      class="home--blog--container"
      v-for="(blogList, index) in blogLists"
      v-bind:key="index"
      v-on:click="changeRoute(blogList)"
    >
      <div class="home--blogtext--container">
        <p style="font-weight: bold;">{{ blogList.title }}</p>
        <p>
          {{ blogList.subtitle }}
        </p>
        <p style="font-size: 13px; font-weight: bold;">
          {{ blogList.author }}
        </p>
        <p style="font-size: 13px;">
          {{ blogList.created_time | moment("LL") }}
        </p>
      </div>
      <div>
        <img
          :src="getImgUrl(blogList)"
          alt=""
          srcset=""
          style="width: 152px; height: 100%;"
        />
      </div>
    </div>
  </div>
</template>

<script>
import BlogService from '@/services/api/index'

export default {
  name: 'HelloWorld',
  created: async function () {
    const { data } = await BlogService.getBlogs()
    const { result } = data
    this.blogLists = result
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      blogLists: [
        {
          id: 1,
          title: 'Creating Async Vue Components',
          subTitle:
            'We use it to save initial loading time and give user a good experience.',
          author: 'The Art',
          img: '1601399329957.jpeg',
          createDate: 'September 11, 2020'
        },
        {
          id: 2,
          title: 'Creating Async Vue Components',
          subTitle:
            'We use it to save initial loading time and give user a good experience.',
          author: 'The Art',
          img: '1601399329957.jpeg',
          createDate: 'September 11, 2020'
        },
        {
          id: 3,
          title: 'Creating Async Vue Components',
          subTitle:
            'We use it to save initial loading time and give user a good experience.',
          author: 'The Art',
          img: '1601399329957.jpeg',
          createDate: 'September 11, 2020'
        }
      ]
    }
  },
  computed: {},
  methods: {
    changeRoute: function (param) {
      if (param) {
        const replaceBlank = param.title
          .split(' ')
          .join('-')
          .toLowerCase()
          .replace(/[^\w\s]/gi, '')
        const path = `${replaceBlank}/${param.id}`
        this.$router.push({ path })
      }
    },
    onCreate: function () {
      this.$router.push({ path: 'create-blog' })
    },
    getImgUrl: function (blog) {
      return `${process.env.BLOG_API}/uploads/${blog.img}`
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.home--blog--container {
  display: flex;
  flex-direction: row;
  text-align: left;
  justify-content: space-between;
  padding: 5px;
  margin: 5px;
  cursor: pointer;
  min-width: 650px;
  max-width: 750px;
  border: solid black 0.5px;
}
.home--create--btn {
  text-align: end;
  padding-right: 5px;
}
.home--blogtext--container {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
}
</style>
