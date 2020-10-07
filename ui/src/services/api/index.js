import axios from 'axios'

const instance = axios.create({
  baseURL: process.env.BLOG_API
})

export default {
  async getBlogs () {
    const result = await instance.get('/')
    return result
  },
  async createBlog (param) {
    const result = await instance.post('/create-blog', param)
    return result
  },
  async uploadImage (formData) {
    try {
      return await instance.post('/uploadimg', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
    } catch (e) {
      return null
    }
  },
  async getDetail (param) {
    try {
      return await instance.post('/detail', param)
    } catch (e) {
      return null
    }
  },
  async deleteBlog (param) {
    try {
      return await instance.post('/delete-blog', param)
    } catch (e) {
      return null
    }
  },
  async updateBlog (param) {
    const result = await instance.post('/update-blog', param)
    return result
  }
}
