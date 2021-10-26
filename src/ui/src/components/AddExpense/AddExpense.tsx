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
          <label htmlFor="isWeeklyExpense">Is a weekly expense?</label>
          <input
            type="checkbox"
            value="yes"
            {...register("isWeeklyExpense")}
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
          <label htmlFor="expense-store">Expense store</label>
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
          <label htmlFor="Amount">Amount</label>
          <input type="number" placeholder="Amount" {...register("Amount", {required: true})} />
        </div>
        <div>
          <label htmlFor="Description">Description</label>
          <textarea {...register("Description", {required: true})} />
        </div>
        <input type="submit" />
      </form>
    </div>
  );
}

export default AddExpense;
