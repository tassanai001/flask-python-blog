<template>
  <div>
    <div v-if="!isEmptyBlog">
      <div class="detail--blog--btn">
        <b-button type="is-info" @click="onBack">
          <font-awesome-icon icon="arrow-left" />
        </b-button>
        <div>
          <b-button type="is-warning" @click="onUpdate">
            <font-awesome-icon icon="cog" />
          </b-button>
          <b-button type="is-danger" @click="onDelete">
            <font-awesome-icon icon="trash" />
          </b-button>
        </div>
      </div>
      <div class="detail--blog--perent">
        {{ blogDetail.title }}
        <div class="detail--blog--author">
          <div>
            {{ blogDetail.author }}
          </div>
          <div>
            {{ blogDetail.created_time }}
          </div>
        </div>
        <div class="detail--blog--img">
          <img :src="getImgUrl(blogDetail)" alt="" srcset="" />
        </div>
        <div class="detail--blog--desc">
          {{ blogDetail.subtitle }} <br />
          {{ blogDetail.detail }}
        </div>
      </div>
    </div>
    <v-dialog />
  </div>
</template>

<script>
import BlogService from '@/services/api/index'

export default {
  name: 'BlogDetail',
  components: {},
  created: async function () {
    const { id } = this.$route.params
    if (id) {
      const response = await BlogService.getDetail({ id })
      if (response) {
        const { data } = response
        data['created_time'] = this.$moment(data['created_time']).format('LL')
        this.blogDetail = data
      } else {
        this.isEmptyBlog = true
        this.$router.push({ path: '/notfound' })
      }
    }
  },
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      blogDetail: {
        title: 'Creating Async Vue Components',
        subTitle:
          'We use it to save initial loading time and give user a good experience.',
        author: 'The Art',
        img: 'https://miro.medium.com/max/10944/0*hZUqzF4Zaz1HSF7X',
        createDate: 'September 11, 2020',
        details: `Vue is an easy front end framework to work with. It lets us create apps easily.
                However, there are still many things that we should look out for when we write apps with them.
                In this article, we’ll look at some essential rules that we should follow when we’re building our Vue apps.
                No async Function for Computed Properties
                The functions we use for computed properties should be synchronous.
                If we use async functions, unexpected behavior may occur.
                If we ned computed properties to be async, then we can use plugins to use them.
                For instance, we should write`
      },
      isEmptyBlog: false,
      isRemoveError: false,
    }
  },
  methods: {
    onDelete: function () {
      this.$modal.show('dialog', {
        title: 'Confirmation',
        text: 'Are you sure you want to delete this blog?',
        buttons: [
          {
            title: 'Yes',
            handler: async () => {
              if (this.blogDetail.id) {
                this.$modal.hideAll()
                const { id } = this.blogDetail
                await BlogService.deleteBlog({ id })
                this.$router.push({ path: '/' })
              }
            }
          },
          {
            title: 'No',
            handler: () => {
              this.$modal.hide('dialog')
            }
          }
        ]
      })
    },
    onUpdate: function () {
      const blogID = this.blogDetail.id
      this.$router.push({ path: `/update-blog/${blogID}` })
    },
    onBack: function () {
      this.$router.go(-1)
    },
    getImgUrl: function (blog) {
      return `${process.env.BLOG_API}/uploads/${blog.img}`
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.detail--blog--author {
  text-align: left;
  margin-top: 32px;
}
.detail--blog--perent {
  display: flex;
  max-width: 680px;
  justify-content: center;
  flex-direction: column;
}
.detail--blog--img {
  margin-top: 25px;
}
.detail--blog--desc {
  margin-top: 25px;
  text-align: left;
}
.detail--blog--btn {
  display: flex;
  justify-content: space-between;
}
</style>
