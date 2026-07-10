# End-to-End Form Creation Workflow (All Steps Required)

Step-by-step guide for creating a new form with validation.

---

## Folder Structure

```
apps/frontend/src/
├── types/
│   └── [domain]FormTypes.ts       # Form data types
├── lib/validations/
│   └── [domain]Schemas.ts         # Yup validation schemas
├── hooks/[domain]/
│   ├── forms/
│   │   └── use[Name]Form.ts       # Form hook (react-hook-form)
│   └── use[Action].ts             # Mutation hook (API call)
└── components/[domain]/
    └── [Name]Form.tsx             # Form component
```

---

## Step 1: Define Form Types

```typescript
// apps/frontend/src/types/projectFormTypes.ts
import type {
  CreateProjectBody,
  UpdateProjectBody,
  ChangePasswordBody,
} from '@backend/types/client';

// Pattern A: Re-export API type directly (when form matches API exactly)
export type CreateProjectFormData = CreateProjectBody;
export type UpdateProjectFormData = UpdateProjectBody;

// Pattern B: Extend API type (when form needs additional fields)
export type ChangePasswordFormData = ChangePasswordBody & {
  confirmPassword: string;  // Form-only field, not sent to API
};

// Pattern C: Pick specific fields from API type
export type QuickEditFormData = Pick<UpdateProjectBody, 'name' | 'status'>;
```

---

## Step 2: Create Validation Schema

```typescript
// apps/frontend/src/lib/validations/projectSchemas.ts
import * as yup from 'yup';

export const createProjectSchema = yup.object({
  // Required string with length validation
  name: yup.string().required('Required').min(2, 'Min 2 chars').max(255, 'Max 255 chars').trim(),

  // Optional string
  description: yup.string().max(1000, 'Max 1000 chars').notRequired(),

  // Email
  email: yup.string().required('Required').email('Invalid email').trim(),

  // Password with pattern
  password: yup.string().required('Required').min(8, 'Min 8 chars')
    .matches(/^(?=.*[A-Za-z])(?=.*\d).+$/, 'Must contain letter and number'),

  // Confirm field (must match another field)
  confirmPassword: yup.string().required('Required')
    .oneOf([yup.ref('password')], 'Passwords must match'),

  // Enum/select
  role: yup.string().oneOf(['admin', 'member'], 'Invalid').required('Required'),

  // Optional URL
  url: yup.string().url('Invalid URL').notRequired(),
});
```

---

## Step 3: Create Form Hook

```typescript
// apps/frontend/src/hooks/project/forms/useCreateProjectForm.ts
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { createProjectSchema } from '@/lib/validations/projectSchemas';
import type { CreateProjectFormData } from '@/types/projectFormTypes';

export function useCreateProjectForm() {
  return useForm<CreateProjectFormData>({
    resolver: yupResolver(createProjectSchema),
    mode: 'onChange',
    defaultValues: { name: '', description: '' },
  });
}

// With initial data (for edit forms)
export function useUpdateProjectForm(project?: Project) {
  return useForm<UpdateProjectFormData>({
    resolver: yupResolver(updateProjectSchema),
    mode: 'onChange',
    defaultValues: {
      name: project?.name || '',
      description: project?.description || '',
    },
  });
}
```

---

## Step 4: Create Mutation Hook

> **Use the `api-integration` skill** for creating mutation hooks.
> Follow Steps 2-4 in `api-integration` workflow for service method, query keys, and mutation hook.

---

## Step 5: Create Form Component

```typescript
// apps/frontend/src/components/project/CreateProjectForm.tsx
'use client';

import { Card, CardContent, CardHeader, CardTitle, Input, Select, ButtonWithLoader } from '@/components';
import { useCreateProjectForm } from '@/hooks/project/forms/useCreateProjectForm';
import { useCreateProjectMutation } from '@/hooks/project/useProjectMutations';
import useMultiLanguage from '@/hooks/useMultiLanguage';
import type { CreateProjectFormData } from '@/types/projectFormTypes';

interface CreateProjectFormProps {
  onSuccess?: () => void;
}

export function CreateProjectForm({ onSuccess }: CreateProjectFormProps) {
  const { LABELS, PLACEHOLDERS, BUTTONS } = useMultiLanguage();
  const { mutate: createProject, isPending: isLoading } = useCreateProjectMutation();
  const { register, handleSubmit, reset, watch, formState: { errors } } = useCreateProjectForm();

  // Watch field for dependent field logic
  const visibility = watch('visibility');

  const onSubmit = (data: CreateProjectFormData) => {
    createProject(data, { onSuccess: () => { reset(); onSuccess?.(); } });
  };

  return (
    <Card className="glass">
      <CardHeader>
        <CardTitle className="text-base">{LABELS.CREATE_PROJECT}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <Input
            label={LABELS.PROJECT_NAME}
            placeholder={PLACEHOLDERS.ENTER_PROJECT_NAME}
            disabled={isLoading}
            error={errors.name?.message}
            {...register('name')}
          />
          <Select
            label={LABELS.VISIBILITY}
            disabled={isLoading}
            error={errors.visibility?.message}
            {...register('visibility')}
          >
            <option value="public">{LABELS.PUBLIC}</option>
            <option value="private">{LABELS.PRIVATE}</option>
          </Select>

          {/* Dependent field: only show when visibility is 'private' */}
          {visibility === 'private' && (
            <Select
              label={LABELS.TEAM}
              disabled={isLoading}
              error={errors.teamId?.message}
              {...register('teamId')}
            >
              {/* Options from teams query */}
            </Select>
          )}

          <ButtonWithLoader type="submit" variant="hero" isLoading={isLoading} loadingText={BUTTONS.CREATING}>
            {BUTTONS.CREATE_PROJECT}
          </ButtonWithLoader>
        </form>
      </CardContent>
    </Card>
  );
}
```

> **Use the `translation` skill (Required)** to add new translation keys (LABELS, PLACEHOLDERS, BUTTONS).

---

## Step 6: Add to Barrel Exports

```typescript
// components/project/index.ts
export { CreateProjectForm } from './CreateProjectForm';

// components/index.ts
export * from './project';
```

---

## Checklist

- [ ] Form types in `types/[domain]FormTypes.ts` (re-export or extend API types)
- [ ] Validation schema in `lib/validations/[domain]Schemas.ts`
- [ ] Form hook in `hooks/[domain]/forms/use[Name]Form.ts`
- [ ] Mutation hook via `api-integration` skill
- [ ] Form component with `'use client'` directive
- [ ] Inputs: `error={errors.field?.message}`, `disabled={isLoading}`
- [ ] Submit: `ButtonWithLoader` with `loadingText`
- [ ] Added to barrel exports
- [ ] Translations via `translation` skill
