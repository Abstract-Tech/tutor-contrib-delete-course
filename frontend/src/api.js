import { getConfig } from '@edx/frontend-platform';
import { getAuthenticatedHttpClient } from '@edx/frontend-platform/auth';

const getApiBaseUrl = () => getConfig().STUDIO_BASE_URL;

export const getDeleteCourseApiUrl = (courseId) => {
  const encodedCourseId = encodeURIComponent(courseId);
  return `${getApiBaseUrl()}/delete_course_plugin/v1/courses/${encodedCourseId}/delete/`;
};

export async function canDeleteCourse(courseId) {
  const { data } = await getAuthenticatedHttpClient().get(
    getDeleteCourseApiUrl(courseId),
  );
  return data;
}

export async function deleteCourse(courseId, { reason = '' } = {}) {
  const { data } = await getAuthenticatedHttpClient().post(
    getDeleteCourseApiUrl(courseId),
    {
      reason,
    },
  );

  return data;
}
