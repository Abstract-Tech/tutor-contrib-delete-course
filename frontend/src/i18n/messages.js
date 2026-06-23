import { defineMessages } from '@edx/frontend-platform/i18n';

const messages = defineMessages({
  unableToResolveCourseId: {
    id: "courseDelete.unableToResolveCourseId",
    defaultMessage: "Unable to resolve course ID.",
    description: "Alert shown when course ID cannot be inferred for deletion.",
  },
  failedToDeleteCourse: {
    id: "courseDelete.failedToDeleteCourse",
    defaultMessage: "Failed to delete course.",
    description: "Fallback error message shown when delete request fails.",
  },
  deleteCourseButton: {
    id: "courseDelete.deleteCourseButton",
    defaultMessage: "Delete Course",
    description:
      "Danger button text used to open deletion modal and confirm delete.",
  },
  deletingButton: {
    id: "courseDelete.deletingButton",
    defaultMessage: "Deleting...",
    description: "Button text shown while deletion is in progress.",
  },
  modalTitle: {
    id: "courseDelete.modalTitle",
    defaultMessage: "Delete course permanently?",
    description: "Delete confirmation modal title.",
  },
  modalMessage: {
    id: "courseDelete.modalMessage",
    defaultMessage:
      "This action permanently deletes all course data. Export or back up the course first if you may need it later. This action cannot be undone.",
    description: "Main warning message in course delete confirmation modal.",
  },
  courseIdLabel: {
    id: "courseDelete.courseIdLabel",
    defaultMessage: "Course ID",
    description: "Label for the readonly resolved course ID value.",
  },
  courseIdConfirmLabel: {
    id: "courseDelete.courseIdConfirmLabel",
    defaultMessage:
      "Security check: Type the exact course ID to confirm deletion.",
    description: "Label for course ID confirmation input.",
  },
  courseIdConfirmPlaceholder: {
    id: "courseDelete.courseIdConfirmPlaceholder",
    defaultMessage: "Enter exact course ID",
    description: "Placeholder for course ID confirmation input.",
  },
  reasonPrompt: {
    id: "courseDelete.reasonPrompt",
    defaultMessage: "Optional: Add a deletion reason for the admin audit log.",
    description: "Label for optional delete reason textarea.",
  },
  cancelButton: {
    id: "courseDelete.cancelButton",
    defaultMessage: "Cancel",
    description: "Cancel button text in delete confirmation modal.",
  },
});

export default messages;
