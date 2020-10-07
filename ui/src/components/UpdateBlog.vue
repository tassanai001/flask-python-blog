<template>
  <div>
    <b-field
      label="Title"
      :label-position="labelPosition"
      :type="formValidate.title.inputType"
      class="createpost--form"
      :message="formValidate.title.message"
    >
      <b-input
        v-model="title"
        class="createpost--form"
        @input="onHandleValid('title')"
      ></b-input>
    </b-field>

    <b-field
      label="Subtitle"
      :label-position="labelPosition"
      :type="formValidate.subtitle.inputType"
      class="createpost--form"
      :message="formValidate.subtitle.message"
    >
      <b-input
        v-model="subtitle"
        class="createpost--form"
        @input="onHandleValid('subtitle')"
      ></b-input>
    </b-field>

    <b-field class="createpost--form">
      <div>
        <b-upload v-model="dropFiles" multiple drag-drop>
          <section class="section createpost--form">
            <div class="content has-text-centered">
              <p>Drop your files here or click to upload</p>
            </div>
          </section>
        </b-upload>
        <p class="help is-danger" v-if="!img">
          This image is required
        </p>
      </div>
    </b-field>

    <div class="updateblog--img--preview">
      <div class="updateblog--img--preview--container">
        <img v-if="img" :src="getImgUrl()" />
      </div>
    </div>

    <b-field
      label="Detail"
      :label-position="labelPosition"
      class="createpost--form"
      :type="formValidate.detail.inputType"
      :message="formValidate.detail.message"
    >
      <b-input
        v-model="detail"
        @input="onHandleValid('detail')"
        class="createpost--form"
        type="textarea"
      >
      </b-input>
    </b-field>

    <b-field
      label="Author"
      :label-position="labelPosition"
      class="createpost--form"
      :type="formValidate.author.inputType"
      :message="formValidate.author.message"
    >
      <b-input
        v-model="author"
        @input="onHandleValid('author')"
        class="createpost--form"
      >
      </b-input>
    </b-field>

    <div class="updateblog--btn--action">
      <b-button type="is-primary" @click="onUpdate">Update</b-button>
      <b-button type="is-warning" @click="onCancel">Cancel</b-button>
    </div>
    <v-dialog />
  </div>
</template>

<script>
import BlogService from '@/services/api/index'

export default {
  name: 'UpdateBlog',
  components: {},
  created: async function () {
    const { id } = this.$route.params
    if (id) {
      const response = await BlogService.getDetail({ id })
      if (response) {
        const { data } = response
        this.title = data.title
        this.detail = data.detail
        this.subtitle = data.subtitle
        this.author = data.author
        this.img = data.img
        this.id = data.id
      } else {
        this.isEmptyBlog = true
        this.$router.push({ path: '/notfound' })
      }
    }
  },
  data () {
    return {
      labelPosition: 'on-border',
      title: null,
      detail: null,
      subtitle: null,
      author: null,
      img: null,
      id: null,
      formValidate: {
        title: {
          inputType: '',
          message: ''
        },
        subtitle: {
          inputType: '',
          message: ''
        },
        detail: {
          inputType: '',
          message: ''
        },
        author: {
          inputType: '',
          message: ''
        }
      },
      dropFiles: []
    }
  },
  methods: {
    onUpdate: async function (e) {
      if (!this.title) {
        this.formValidate.title.inputType = 'is-danger'
        this.formValidate.title.message = 'This title is required'
        return false
      }

      if (!this.subtitle) {
        this.formValidate.subtitle.inputType = 'is-danger'
        this.formValidate.subtitle.message = 'This subtitle is required'
        return false
      }

      if (!this.detail) {
        this.formValidate.detail.inputType = 'is-danger'
        this.formValidate.detail.message = 'This detail is required'
        return false
      }

      if (!this.author) {
        this.formValidate.author.inputType = 'is-danger'
        this.formValidate.author.message = 'This author is required'
        return false
      }

      if (!this.img) {
        return
      }

      let fileName = ''
      const fileType =
        this.dropFiles.length > 0 ? this.dropFiles[0].type : null
      if (fileType) {
        fileName = `${Number(new Date()).toString()}.${
          fileType.split('/')[1]
        }`
      } else {
        fileName = this.img
      }

      const createParam = {
        title: this.title,
        detail: this.detail,
        subtitle: this.subtitle,
        author: this.author,
        img: fileName,
        id: this.id
      }

      e.preventDefault()
      const response = await BlogService.updateBlog(createParam)
      if (response.status === 200) {
        const fileUpload = this.dropFiles.length > 0 ? this.dropFiles[0] : null
        let formData = new FormData()
        formData.append('file', fileUpload, fileName)
        const uploadResponse = await BlogService.uploadImage(formData)
        if (uploadResponse.status === 200) {
          this.$router.push({ path: '/' })
        } else {
          console.log('error')
        }
      }
    },
    onHandleValid: function (type) {
      if (!this[type]) {
        this.formValidate[type].inputType = 'is-danger'
        this.formValidate[type].message = `This ${type} is required`
      } else {
        this.formValidate[type].inputType = ''
        this.formValidate[type].message = ''
      }
    },
    uploadImage (event) {
      console.log(event.target.files[0])
    },
    getImgUrl () {
      if (this.dropFiles.length > 0) {
        const file = this.dropFiles[0]
        const fileName =
          this.dropFiles.length > 0 ? this.dropFiles[0].name : null
        this.img = fileName
        return URL.createObjectURL(file)
      } else {
        return `${process.env.BLOG_API}/uploads/${this.img}`
      }
    },
    onCancel () {
      this.$router.push({ path: '/' })
    }
  }
}
</script>

<style scoped>
.createpost--form {
  text-align: left;
  min-width: 500px;
}
.updateblog--img--preview {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0.75rem;
}
.updateblog--img--preview > .updateblog--img--preview--container > img {
  max-width: 100%;
  max-height: 120px;
}
.updateblog--img--preview--container {
  display: flex;
  position: relative;
}
.updateblog--btn--action {
  display: flex;
  justify-content: space-between;
  flex-direction: row;
}
</style>
