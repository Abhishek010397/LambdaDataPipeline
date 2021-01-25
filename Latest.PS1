$latest=(gci c:\temp | ? { $_.PSIsContainer } | sort CreationTime)[-1] | Select -ExpandProperty Name

aws s3 cp C:\Users\Abhi\$latest s3://bucket-name/$latest
