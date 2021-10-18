import { Controller, useForm } from "react-hook-form";
import ReactDatePicker from 'react-datepicker'
import './AddExpence.css'
import "react-datepicker/dist/react-datepicker.css";
import ReactSelect from "react-select";

function AddExpense() {
  const { control, register, handleSubmit } = useForm();
  const onSubmit = (data: any) => {
    alert(JSON.stringify(data));
  };

  return (
    <div className="App">
      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
          <label htmlFor="firstName">First Name</label>
          <input placeholder="bill" {...register("firstName")} />
        </div>

        <div>
          <label htmlFor="lastName">Last Name</label>
          <input placeholder="luo" {...register("lastName")} />
        </div>

        <div>
          <label htmlFor="isDeveloper">Is an developer?</label>
          <input
            type="checkbox"
            placeholder="luo"
            value="yes"
            {...register("isDeveloper")}
          />
        </div>
        <div>
          <label htmlFor="expense-date">Expense date</label>
        <Controller
          control={control}
          name='date-input'
          render={({ field }) => (
            <ReactDatePicker
              placeholderText='Select date'
              onChange={(date: any) => field.onChange(date)}
              selected={field.value}
            />
        )}
        />
        </div>
        <div>
          <label htmlFor="expense-category">Expense category</label>
        <Controller
          render={({ field }) => (
            <ReactSelect
              {...field}
              options={[
                { value: "chocolate", label: "Chocolate" },
                { value: "strawberry", label: "Strawberry" },
                { value: "vanilla", label: "Vanilla" }
              ]}
              isClearable
            />
          )}
          name="ReactSelect"
          control={control}
        />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            placeholder="bluebill1049@hotmail.com"
            type="email"
            {...register("email")}
          />
        </div>
        <input type="submit" />
      </form>
    </div>
  );
}

export default AddExpense;
