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
              <font-awesome-icon icon="arrow-up" size="lg" />
              <p>Drop your files here or click to upload</p>
            </div>
          </section>
        </b-upload>
        <p class="help is-danger" v-if="!img && isSubmit">
          This image is required
        </p>
      </div>
    </b-field>

    <div class="createblog--img--preview">
      <div class="createblog--img--preview--container">
        <img v-if="dropFiles.length > 0" :src="getImgUrl()" />
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

    <b-button type="is-primary" @click="checkForm">Create</b-button>
    <v-dialog />
  </div>
</template>

<script>
import BlogService from '@/services/api/index'

export default {
  components: {},
  data () {
    return {
      labelPosition: 'on-border',
      title: null,
      detail: null,
      subtitle: null,
      author: null,
      img: null,
      isSubmit: false,
      formValid: true,
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
    deleteDropFile: function (index) {
      this.dropFiles.splice(index, 1)
    },
    checkForm: async function (e) {
      this.isSubmit = true
      this.formValid = true

      if (!this.title) {
        this.formValidate.title.inputType = 'is-danger'
        this.formValidate.title.message = 'This title is required'
        this.formValid = false
      }

      if (!this.subtitle) {
        this.formValidate.subtitle.inputType = 'is-danger'
        this.formValidate.subtitle.message = 'This subtitle is required'
        this.formValid = false
      }

      if (!this.detail) {
        this.formValidate.detail.inputType = 'is-danger'
        this.formValidate.detail.message = 'This detail is required'
        this.formValid = false
      }

      if (!this.author) {
        this.formValidate.author.inputType = 'is-danger'
        this.formValidate.author.message = 'This author is required'
        this.formValid = false
      }

      if (!this.formValid) {
        return false
      }

      const fileType =
        this.dropFiles.length > 0 ? this.dropFiles[this.dropFiles.length - 1].type : null
      const fileName = `${Number(new Date()).toString()}.${
        fileType.split('/')[1]
      }`

      const createParam = {
        title: this.title,
        detail: this.detail,
        subtitle: this.subtitle,
        author: this.author,
        img: fileName
      }

      e.preventDefault()

      const response = await BlogService.createBlog(createParam)
      if (response.status === 200) {
        const fileUpload = this.dropFiles.length > 0 ? this.dropFiles[this.dropFiles.length - 1] : null
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
    getImgUrl () {
      if (this.dropFiles.length > 0) {
        const file = this.dropFiles[this.dropFiles.length - 1]
        const fileName =
          this.dropFiles.length > 0 ? this.dropFiles[this.dropFiles.length - 1].name : null
        this.img = fileName
        return URL.createObjectURL(file)
      } else {
        return `${process.env.BLOG_API}/uploads/${this.img}`
      }
    }
  }
}
</script>

<style scoped>
.createpost--form {
  text-align: left;
  min-width: 500px;
}
.createblog--img--preview {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 0.75rem;
}
.createblog--img--preview > .createblog--img--preview--container > img {
  max-width: 100%;
  max-height: 120px;
}
.createblog--img--preview--container {
  display: flex;
  position: relative;
}
</style>
