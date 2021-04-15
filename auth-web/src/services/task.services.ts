import { Task, TaskFilterParams, TaskList } from '@/models/Task'

import { AxiosResponse } from 'axios'
import ConfigHelper from '@/util/config-helper'
import { axios } from '@/util/http-util'

export default class TaskService {
  public static async getTaskById (taskId: number): Promise<AxiosResponse<Task>> {
    return axios.get(`${ConfigHelper.getAuthAPIUrl()}/tasks/${taskId}`)
  }

  public static async fetchTasks (taskFilter?: TaskFilterParams): Promise<AxiosResponse<TaskList>> {
    let params = new URLSearchParams()
    if (taskFilter.status) {
      params.append('status', taskFilter.status)
    }
    if (taskFilter.type) {
      params.append('type', taskFilter.type)
    }
    if (taskFilter.pageNumber) {
      params.append('page', taskFilter.pageNumber.toString())
    }
    if (taskFilter.pageLimit) {
      params.append('limit', taskFilter.pageLimit.toString())
    }

    return axios.get(`${ConfigHelper.getAuthAPIUrl()}/tasks`, { params })
  }

  static async approvePendingTask (task:any): Promise<AxiosResponse> {
    const taskId = task.id
    return axios.put(`${ConfigHelper.getValue('VUE_APP_AUTH_ROOT_API')}/tasks/${taskId}`, { ...task, relationshipStatus: 'APPROVED' })
  }

  static async rejectPendingTask (task:any): Promise<AxiosResponse> {
    const taskId = task.id
    return axios.put(`${ConfigHelper.getValue('VUE_APP_AUTH_ROOT_API')}/tasks/${taskId}`, { ...task, relationshipStatus: 'REJECTED' })
  }
}
